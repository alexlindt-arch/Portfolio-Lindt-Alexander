#!/usr/bin/env python3
"""Deployt das statische Portfolio per FTPS nach Hostinger.

Zugangsdaten kommen aus deploy/ftp.json (gitignored):
    {"host": "...", "user": "...", "password": "..."}

Ablauf:
    python deploy/deploy_hostinger.py check     # Login + Webroot + Inhalt anzeigen
    python deploy/deploy_hostinger.py backup    # .htaccess + Root-Listing sichern
    python deploy/deploy_hostinger.py stage     # Upload nach /neu/ zum Testen
    python deploy/deploy_hostinger.py golive    # Upload ins Root + .htaccess patchen
    python deploy/deploy_hostinger.py rollback  # .htaccess aus dem Backup zuruecksetzen
"""
import argparse
import ftplib
import io
import json
import os
import posixpath
import ssl
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(ROOT, 'deploy', 'ftp.json')
BACKUP_DIR = os.path.join(ROOT, 'deploy', 'backup')
HTACCESS_BLOCK = os.path.join(ROOT, 'deploy', 'htaccess-block.txt')

FILES = [
    'index.html',
    'Portfolio Desktop.dc.html',
    'Portfolio Mobile.dc.html',
    'robots.txt',
    'sitemap.xml',
]
DIRS = ['scripts', 'assets']

WEBROOT_CANDIDATES = [
    '/public_html',
    '/domains/alexanderlindtwebdesign.com/public_html',
    '/home/public_html',
    '.',
]
MARKER = '# BEGIN Portfolio-Static'


def load_cfg():
    if not os.path.exists(CFG):
        sys.exit(f"FEHLT: {CFG}\n"
                 'Anlegen mit: {"host": "...", "user": "...", "password": "..."}')
    with open(CFG, encoding='utf-8') as f:
        return json.load(f)


def connect(cfg):
    """FTPS bevorzugt, Fallback auf einfaches FTP."""
    host, user, pw = cfg['host'], cfg['user'], cfg['password']
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ftp = ftplib.FTP_TLS(context=ctx, timeout=60)
        ftp.connect(host, cfg.get('port', 21))
        ftp.login(user, pw)
        ftp.prot_p()
        print('  Verbindung: FTPS (verschluesselt)')
    except Exception as e:
        print(f'  FTPS nicht moeglich ({e}) -> Fallback auf FTP')
        ftp = ftplib.FTP(timeout=60)
        ftp.connect(host, cfg.get('port', 21))
        ftp.login(user, pw)
    ftp.set_pasv(True)
    return ftp


def listing(ftp, path='.'):
    try:
        return ftp.nlst(path)
    except ftplib.error_perm:
        return []


def find_webroot(ftp):
    """Verzeichnis finden, in dem WordPress bzw. der Domain-Root liegt."""
    start = ftp.pwd()
    for cand in WEBROOT_CANDIDATES:
        try:
            ftp.cwd(cand if cand != '.' else start)
        except ftplib.error_perm:
            continue
        names = {posixpath.basename(n) for n in listing(ftp)}
        if 'wp-config.php' in names or 'wp-load.php' in names or 'index.php' in names:
            return ftp.pwd()
    sys.exit('Kein Webroot gefunden. Bitte den Pfad manuell in ftp.json als "webroot" setzen.')


def ensure_dir(ftp, remote_dir):
    parts = [p for p in remote_dir.split('/') if p]
    cur = '/' if remote_dir.startswith('/') else ''
    for p in parts:
        cur = posixpath.join(cur, p) if cur else p
        try:
            ftp.mkd(cur)
        except ftplib.error_perm:
            pass


def upload_file(ftp, local, remote):
    size = os.path.getsize(local)
    with open(local, 'rb') as f:
        ftp.storbinary(f'STOR {remote}', f, blocksize=65536)
    print(f'    {posixpath.basename(remote):<40} {size:>9,} B')


def upload_tree(ftp, local_dir, remote_dir):
    ensure_dir(ftp, remote_dir)
    for entry in sorted(os.listdir(local_dir)):
        lp = os.path.join(local_dir, entry)
        rp = posixpath.join(remote_dir, entry)
        if os.path.isdir(lp):
            upload_tree(ftp, lp, rp)
        else:
            upload_file(ftp, lp, rp)


def read_remote(ftp, remote):
    buf = io.BytesIO()
    try:
        ftp.retrbinary(f'RETR {remote}', buf.write)
    except ftplib.error_perm:
        return None
    return buf.getvalue()


def write_remote(ftp, remote, data: bytes):
    ftp.storbinary(f'STOR {remote}', io.BytesIO(data))


def cmd_check(ftp, webroot, _args):
    print(f'\nWebroot: {webroot}\n')
    ftp.cwd(webroot)
    for n in sorted(posixpath.basename(x) for x in listing(ftp)):
        print('  ' + n)


def cmd_backup(ftp, webroot, _args):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    ht = read_remote(ftp, posixpath.join(webroot, '.htaccess'))
    if ht is None:
        print('  Kein .htaccess vorhanden (wird beim golive neu angelegt)')
        ht = b''
    dst = os.path.join(BACKUP_DIR, f'htaccess-{stamp}.bak')
    with open(dst, 'wb') as f:
        f.write(ht)
    print(f'  .htaccess gesichert -> {dst} ({len(ht)} B)')

    ftp.cwd(webroot)
    names = sorted(posixpath.basename(x) for x in listing(ftp))
    dst2 = os.path.join(BACKUP_DIR, f'root-listing-{stamp}.txt')
    with open(dst2, 'w', encoding='utf-8') as f:
        f.write('\n'.join(names))
    print(f'  Root-Listing gesichert -> {dst2} ({len(names)} Eintraege)')


def _upload_payload(ftp, target):
    ensure_dir(ftp, target)
    print(f'\n  Ziel: {target}')
    for name in FILES:
        lp = os.path.join(ROOT, name)
        if os.path.exists(lp):
            upload_file(ftp, lp, posixpath.join(target, name))
    for d in DIRS:
        lp = os.path.join(ROOT, d)
        if os.path.isdir(lp):
            print(f'    -- {d}/ --')
            upload_tree(ftp, lp, posixpath.join(target, d))


def cmd_stage(ftp, webroot, args):
    target = posixpath.join(webroot, args.dir)
    _upload_payload(ftp, target)
    with open(HTACCESS_BLOCK, 'rb') as f:
        block = f.read()
    write_remote(ftp, posixpath.join(target, '.htaccess'), block)
    print(f'\n  Testen unter: https://alexanderlindtwebdesign.com/{args.dir}/')


def cmd_golive(ftp, webroot, _args):
    _upload_payload(ftp, webroot)

    ht_path = posixpath.join(webroot, '.htaccess')
    current = read_remote(ftp, ht_path) or b''
    if MARKER.encode() in current:
        print('\n  .htaccess enthaelt den Block bereits - unveraendert')
    else:
        with open(HTACCESS_BLOCK, 'rb') as f:
            block = f.read()
        new = current.rstrip(b'\r\n') + b'\n\n' + block
        write_remote(ftp, ht_path, new)
        print(f'\n  .htaccess ergaenzt ({len(current)} -> {len(new)} B)')
    print('\n  Live: https://alexanderlindtwebdesign.com/')


def cmd_rollback(ftp, webroot, _args):
    baks = sorted(f for f in os.listdir(BACKUP_DIR) if f.startswith('htaccess-'))
    if not baks:
        sys.exit('Kein Backup gefunden.')
    src = os.path.join(BACKUP_DIR, baks[-1])
    with open(src, 'rb') as f:
        data = f.read()
    write_remote(ftp, posixpath.join(webroot, '.htaccess'), data)
    print(f'  .htaccess zurueckgesetzt aus {baks[-1]} ({len(data)} B)')
    print('  Hinweis: index.html liegt weiterhin im Root und muesste zusaetzlich')
    print('  geloescht/umbenannt werden, damit WordPress die Startseite wieder rendert.')


COMMANDS = {
    'check': cmd_check,
    'backup': cmd_backup,
    'stage': cmd_stage,
    'golive': cmd_golive,
    'rollback': cmd_rollback,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=COMMANDS)
    ap.add_argument('--dir', default='neu', help='Unterordner fuer "stage" (Default: neu)')
    args = ap.parse_args()

    cfg = load_cfg()
    print(f'Verbinde mit {cfg["host"]} als {cfg["user"]} ...')
    ftp = connect(cfg)
    try:
        webroot = cfg.get('webroot') or find_webroot(ftp)
        COMMANDS[args.command](ftp, webroot, args)
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()


if __name__ == '__main__':
    main()
