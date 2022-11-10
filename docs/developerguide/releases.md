# Managing Releases

*These instructions are primarily intended for the maintainers of Teamware.*

Note: Releases are always made from the `master` branch of the repository.

## Steps to making a release

1. **Update the changelog** - This has to be done manually, go through any pull requests to `dev` since the last release. Include the changes in the `CHANGELOG` file and in the release notes later.    
1. **Update and check the version numbers** - from the teamware directory run `python version.py check` to check whether all version numbers are up to date. If not, update the master `VERSION` file and run `python version.py update` to update all other version numbers and commit the result. Note that `version.py` requires `pyyaml` for reading `CITATION.cff`, `pyyaml` is included in Teamware's dependencies.
1. **Create a pull request from `dev` to `master`** including any changes to `CHANGELOG`, `VERSION`.
1. **Creating a release** - Create a release via the GitHub interface, the relevant commit can be tagged at this stage or prior to creating the release.
