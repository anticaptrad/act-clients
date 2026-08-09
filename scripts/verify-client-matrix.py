#!/usr/bin/env python3
from pathlib import Path
import tomllib
ROOT=Path(__file__).resolve().parents[1]
manifest=tomllib.loads((ROOT/'.zpkg.toml').read_text())
required={'nodejs':'clients/typescript','python':'clients/python','golang':'clients/go','rust':'clients/rust','dart':'clients/dart','ruby':'clients/ruby','php':'clients/php','java':'clients/java','kotlin':'clients/kotlin','csharp':'clients/csharp','swift':'clients/swift','gleam':'clients/gleam','erlang':'clients/erlang','elixir':'clients/elixir','c':'clients/c','cpp':'clients/cpp','zig':'clients/zig','shell':'clients/shell'}
assert manifest.get('install',{}).get('dir')=='.vendor/.zed'
assert set(manifest.get('dependencies',{}))=={'anticaptrad/act-interfaces'}
for key,path in required.items():
    assert manifest['targets'][key]['dir']==path, (key,manifest['targets'].get(key))
    assert (ROOT/path).is_dir(), path
pkg=(ROOT/'clients/typescript/package.json').read_text()
for entry in ['./node','./deno','./bun','./edge']:
    assert entry in pkg, entry
print(f'validated {len(required)} canonical Zed targets plus Node/Deno/Bun/edge exports')
