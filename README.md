# jflei.com

Built on top of <https://github.com/poole/hyde>.

## Locking dependencies

Bundler does not include integrity hashes, so we use `bundix`:

```console
bundix --lock
```

## Development

- `make run` - view <http://localhost:4000>

## Generate thumbnails

- `nix run .#resize-images`
