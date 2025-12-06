Release steps:

- [ ] Create a `release` branch.
- [ ] Increment `PACKAGE_VERSION` in `CMakeLists.txt`.
- [ ] Update version number in Bazel `git_repository` example in `doc/index.html`.
- [ ] Summarize high-level changes since last release in `ChangeLog.txt`.
- [ ] Add a release announcement to `README.md`.
- [ ] Merge `release` branch into `main`.
- [ ] Create a signed Git tag using `git tag -s vX.Y.Z`.
- [ ] Create a new [signed release](https://wiki.debian.org/Creating%20signed%20GitHub%20releases) on GitHub with auto-generation of release notes.
