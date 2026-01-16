import os
import re
import json

VERSIONS_DIR = "alembic/versions"

def read_migration_headers(file_path):
    """Extract revision + down_revision from migration file."""
    with open(file_path, "r") as f:
        content = f.read()

    revision = re.search(r"revision\s*=\s*['\"](.*?)['\"]", content)
    down_rev = re.search(r"down_revision\s*=\s*['\"](.*?)['\"]", content)

    return {
        "file": file_path,
        "revision": revision.group(1) if revision else None,
        "down_revision": down_rev.group(1) if down_rev else None
    }

def load_migrations():
    files = [f"{VERSIONS_DIR}/{x}" for x in os.listdir(VERSIONS_DIR) if x.endswith(".py") and "pycache" not in x]
    migrations = []

    for f in files:
        header = read_migration_headers(f)
        if header["revision"]:
            migrations.append(header)

    return migrations

def detect_head(migrations):
    """Find file whose revision is not referenced by any other."""
    all_revs = {m["revision"] for m in migrations}
    all_down = {m["down_revision"] for m in migrations if m["down_revision"]}

    heads = list(all_revs - all_down)
    return heads[0] if heads else None  # latest migration

def detect_base(migrations):
    """Find file where down_revision == None"""
    for m in migrations:
        if m["down_revision"] is None or m["down_revision"] == "None":
            return m["revision"]
    return None

def sort_chain(migrations):
    """Sort migrations in real migration order."""
    lookup = {m["revision"]: m for m in migrations}
    order = []

    base = detect_base(migrations)
    if not base:
        print("❌ No base migration found! add manually!")
        return []

    current = base
    order.append(lookup[current])

    while True:
        nxt = [m for m in migrations if m["down_revision"] == current]
        if not nxt:
            break
        order.append(nxt[0])
        current = nxt[0]["revision"]

    return order

def fix_down_revisions(sorted_migrations):
    """Rewrite down_revision chain sequentially."""
    for i, mig in enumerate(sorted_migrations):
        path = mig["file"]
        with open(path, "r") as f:
            txt = f.read()

        # base migration
        if i == 0:
            txt = re.sub(r"down_revision\s*=\s*['\"].*?['\"]", "down_revision = None", txt)
        else:
            prev_rev = sorted_migrations[i-1]["revision"]
            txt = re.sub(r"down_revision\s*=\s*['\"].*?['\"]", f"down_revision = '{prev_rev}'", txt)

        with open(path, "w") as f:
            f.write(txt)

    print("\n🟢 Migration chain fixed successfully.\n")
    print("👉 Now run:\n")
    print("   alembic stamp head")
    print("   alembic upgrade head\n")


if __name__ == "__main__":
    migrations = load_migrations()

    print(f"Found {len(migrations)} migration files.")

    sorted_migs = sort_chain(migrations)

    if not sorted_migs or len(sorted_migs) != len(migrations):
        print("⚠ Migrations may not be linear — repairing chain anyway...")

    fix_down_revisions(sorted_migs)
