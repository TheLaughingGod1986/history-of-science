"""Verify the two v08 archive rows and rebuild the partial assembly index."""
import json, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
NAS = Path('/Volumes/data/studio-live/History Of Science/02_Video-Projects/011_Surgery-Before-Anaesthesia/07_Edit-Project')
LOCAL = Path('/Volumes/MiniWork/scratch/J2563-archive-v08-assets')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, d):
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')


def main():
    remote = NAS / 'J2563_archive_composites_v08'
    copies = []
    for src in sorted(LOCAL.iterdir()):
        if not src.is_file() or src.name == 'ARCHIVE_COMPOSITES_v08.json':
            continue
        dest = remote / src.name
        assert sha(src) == sha(dest), str(dest)
        copies.append({'name': str(dest.relative_to(NAS)), 'sha256': sha(dest)})
    manifest = json.loads((LOCAL / 'ARCHIVE_COMPOSITES_v08.json').read_text())
    for row in manifest['rows']:
        row['path'] = str(remote / Path(row['path']).name)
        assert sha(Path(row['path'])) == row['sha256']
    save(remote / 'ARCHIVE_COMPOSITES_v08.json', manifest)
    save(HERE / 'ARCHIVE_COMPOSITES_v08.json', manifest)
    copies.append({'name': str((remote / 'ARCHIVE_COMPOSITES_v08.json').relative_to(NAS)), 'sha256': sha(remote / 'ARCHIVE_COMPOSITES_v08.json')})
    plan = json.loads((HERE / 'PICTURE_PLAN_v03.json').read_text())
    indexed = {}
    earlier = [
        ('FREE_GRAPHICS_MANIFEST_v03.json', 'preliminary_free', None),
        ('REMAINING_GRAPHICS_MANIFEST_v04.json', 'preliminary_free', NAS / 'J2563_free_graphics_v04'),
        ('ARCHIVE_COMPOSITES_v06.json', 'preliminary_free', None),
        ('ARCHIVE_COMPOSITES_v07.json', 'preliminary_free', None),
        ('ARCHIVE_COMPOSITES_v08.json', 'preliminary_free', None),
        ('DEPENDENCY_SLATES_v07.json', 'dependency_slate', None),
    ]
    for name, kind, override in earlier:
        for row in json.loads((HERE / name).read_text())['rows']:
            path = Path(row['path'])
            if override:
                path = override / path.name
            assert sha(path) == row['sha256'], str(path)
            assert row['row_id'] not in indexed, row['row_id']
            indexed[row['row_id']] = {'row_id': row['row_id'], 'path': str(path), 'sha256': row['sha256'], 'manifest': name, 'status': kind}
    assert len(indexed) == 88
    missing = [r['row_id'] for r in plan['rows'] if r['row_id'] not in indexed]
    assert missing == [
        'P5:03a_arch_squire_inhaler_1846', 'P5:04a', 'P5:06a_arch_simpson_1847',
        'P5:07a_arch_snow_chloroform_1858', 'P5:14a']
    index = {
        'job': 'J2563', 'plan_sha256': sha(HERE / 'PICTURE_PLAN_v03.json'),
        'status': 'Partial only: 21 preliminary free rows, 67 dependency slates, five archives unbuilt after an HTTP 429; no joined rough',
        'generation_authorized': False, 'film_stage_approved': False, 'audio_review': False, 'motion_review': False,
        'rows': [indexed[r['row_id']] for r in plan['rows'] if r['row_id'] in indexed],
        'missing_rows': missing, 'full_overlay_schedule_complete': False,
        'source_hold': 'Do not request Wikimedia again before 2026-11-13T05:30:00Z. The Squire photograph returned HTTP 429 after the patent and monument files.',
    }
    save(HERE / 'ASSEMBLY_INDEX_v08.json', index)
    verification = {
        'status': 'PASS: two v08 rows copied, 88 NAS row hashes checked, five archives still missing',
        'copy_file_count': len(copies), 'files': copies, 'index_sha256': sha(HERE / 'ASSEMBLY_INDEX_v08.json'),
        'not_reviewed': ['moving_video', 'audio', 'full_overlay_schedule', 'joined_rough'],
    }
    save(HERE / 'J2563_COPY_VERIFICATION_v08.json', verification)
    print(verification['status'])
    print('Still missing:', ', '.join(missing))


if __name__ == '__main__':
    main()
