# Changelog

## [unreleased]
### Added
### Changed
### Fixed

## [0.2.1]
### Added
- Telemetry data sending ([#270](https://github.com/GateNLP/gate-teamware/pull/270))
- Upgrade Docker actions ([#272](https://github.com/GateNLP/gate-teamware/pull/272))
- Allow users to set additional environment variables & gunicorn args when installing with Helm ([#275](https://github.com/GateNLP/gate-teamware/pull/275))
- Documentation versioning ([#276](https://github.com/GateNLP/gate-teamware/pull/276), [#277](https://github.com/GateNLP/gate-teamware/pull/277) & [#285](https://github.com/GateNLP/gate-teamware/pull/285))
- Anonymise annotators by default, with option to deanonymise ([#278](https://github.com/GateNLP/gate-teamware/pull/278))
- Support vertically stacked checkboxes and radio buttons ([#288](https://github.com/GateNLP/gate-teamware/pull/288))


## [0.2.0] - 2022-11-18
### Added
- Added integration tests for annotator leaving project ([#251](https://github.com/GateNLP/gate-teamware/pull/251))
- Added support for document pre-annotation ([#250](https://github.com/GateNLP/gate-teamware/pull/250))
- Better CSV support when configuring the project and when displaying documents and annotations ([#247](https://github.com/GateNLP/gate-teamware/pull/247))
- Added citation information to repository ([#243](https://github.com/GateNLP/gate-teamware/pull/243))
- Added a way to display annotations categories in a specific order ([#234](https://github.com/GateNLP/gate-teamware/pull/234))
- Improvement to Annotator management screen ([#232](https://github.com/GateNLP/gate-teamware/pull/232))
### Changed
- Separate integration tests to make recording optional ([#246](https://github.com/GateNLP/gate-teamware/pull/246))
- Split integration tests by functionality ([#239](https://github.com/GateNLP/gate-teamware/pull/239))
- Moved project cloning function from `teamware.rpc` into `teamware.models.Project` ([#235](https://github.com/GateNLP/gate-teamware/pull/235))
