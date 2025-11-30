# Release instructions

Steps to publish a release (local steps):

1. Ensure tests pass locally:

```powershell
cd backend
python -m pytest tests
```

2. Update `VERSION` if needed.

3. Commit all changes and push to `main`:

```powershell
git add .
git commit -m "chore(release): prepare v$(cat VERSION)"
git push origin main
```

4. Create a Git tag and push it:

```powershell
git tag -a v$(cat VERSION) -m "Release v$(cat VERSION)"
git push origin --tags
```

5. Create a GitHub release from the tag and add release notes (you can use the `CHANGELOG.md`).

CI will run automatically via GitHub Actions to run lint, tests and upload coverage artifacts.
