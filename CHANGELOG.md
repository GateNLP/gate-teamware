# Changelog

## [development]
### Added

### Fixed

## [2.1.0] 2023-05-03

### Added
- Radio buttons and checkbox widgets can optionally have a per-choice helptext tooltip ([#329](https://github.com/GateNLP/gate-teamware/pull/329))

### Changed
- Frontend build chain now uses [Vite](https://vitejs.dev/) ([#342](https://github.com/GateNLP/gate-teamware/pull/342))
- Navbar and footer are now more responsive ([#339](https://github.com/GateNLP/gate-teamware/pull/339))
- Node version upgraded to 18 ([#357](https://github.com/GateNLP/gate-teamware/pull/357))
- Python and Node base images upgraded to used Bullseye Debian ([#357](https://github.com/GateNLP/gate-teamware/pull/357))

### Fixed
- Footer no longer covers over content ([#339](https://github.com/GateNLP/gate-teamware/pull/339))
- Maximum annotations per document limit is no longer erroneously enforced on training and test documents ([#355](https://github.com/GateNLP/gate-teamware/pull/355))
- Release workflow fixed ([#341](https://github.com/GateNLP/gate-teamware/pull/341))

## [2.0.0] 2023-04-13
### Added
- Isolate documentation build chain ([#326](https://github.com/GateNLP/gate-teamware/pull/326))
- Add doi to citation file and doi badge ([#332](https://github.com/GateNLP/gate-teamware/pull/332))
- Add logging and alter data type for telemetry ([#333](https://github.com/GateNLP/gate-teamware/pull/333))
- Add more logging when telemetry is switched off and send_telemetry is called ([#337](https://github.com/GateNLP/gate-teamware/pull/337))

### Changed
- Update node 12 actions to newer node 16 versions ([#334](https://github.com/GateNLP/gate-teamware/pull/334))

### Fixed
- Fix for documentation build breaking ([#336](https://github.com/GateNLP/gate-teamware/pull/336)) 

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
