# Changelog

## [unreleased]
### Added
### Changed
### Fixed

## [0.4.0] 2023-04-03
### Added
- Privacy policy & Terms & Conditions ([#298](https://github.com/GateNLP/gate-teamware/pull/298))
- Helm chart moved to its own repo ([#299](https://github.com/GateNLP/gate-teamware/pull/299))
- Added a cookies policy page ([#301](https://github.com/GateNLP/gate-teamware/pull/301))
- Dynamic options for checkbox/radio/selector ([#303](https://github.com/GateNLP/gate-teamware/pull/303))
- Simpler install process for new users ([#305](https://github.com/GateNLP/gate-teamware/pull/305))
- Multi-arch build support ([#306](https://github.com/GateNLP/gate-teamware/pull/306))
- Added label to the "Other" issue report, converted bold headings to section headers (h2) instead ([#310](https://github.com/GateNLP/gate-teamware/pull/310))
- Add footer link to repository and add a little more info to about page ([#312](https://github.com/GateNLP/gate-teamware/pull/312))
- Allowing users to be deleted from the system ([#318](https://github.com/GateNLP/gate-teamware/pull/318))
- Update the "making a release" documentation to match latest changes ([#319](https://github.com/GateNLP/gate-teamware/pull/319))

### Fixed
- Fixed t.currentAnnotationTask is null error ([#302](https://github.com/GateNLP/gate-teamware/pull/302))
- Don't redeploy docs on push to master  ([#316](https://github.com/GateNLP/gate-teamware/pull/316))
- Admin role should imply manager ([#321](https://github.com/GateNLP/gate-teamware/pull/321))

## [0.3.1] - 2023-02-17
### Fixed
- Missed underscore in documentation link ([#292](https://github.com/GateNLP/gate-teamware/pull/292))

## [0.3.0] - 2023-02-16
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
