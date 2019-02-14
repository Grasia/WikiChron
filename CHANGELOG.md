# Change Log for WikiChron

## 1.1.1 - 2018-10-31
### Added
- Icon in the header which displays a dialog showing sharing and downloading links for current selection. Closes #53
- deps: sd-material-ui
### Changed
- stylesheets and js files divided depending on their scope
- download now returns a zip with one csv per wiki. Re-Closes #21
- moved dump_parser to an independant pypi package and use it as a dependency
- Some improvements in query_bot_users.py script.
### Fixed
- Missing help icons (?) next to the metrics checklist.
### Updated
- deps: dash-core-components, requests.


## 1.1.0 - 2018-10-10
### Added
- Button to download in csv format the current selection of wikis and metrics. See [26](https://github.com/Grasia/WikiChron/issues/26).
- Now the current selection of wikis and metrics is displayed in the URL in the query string section. This allows sharing the your selection with others. See [21](https://github.com/Grasia/WikiChron/issues/21).

### Changed
- File structure of the project. Now the source files are under `wikichron/`.
- Moved main data from hidden div to caching and signaling in server. This commit do the trick: fd0fe05147e9a7546161f2fa232b667dd4dfa1e9. See [this](https://dash.plot.ly/sharing-data-between-callbacks) to learn more about sharing data between callbacks.

### Updated
- deps: dash, dash-renderer, dash-core-components, etc.

## 1.0.0 - 2018-09-05
First stable version with MVP!

- Improvements to the slider. See #22.
- Updated dependencies to last versions
- Clean up of repo and code

## 1.0.0-beta - 2018-09-03
Beta release
- Added multi-user and multi-threading support
- Updated dependencies to last versions
- Inner improvements

## 0.6.2 - 2018-05-22
Beta release
- Fixed small bug when appending external js to_import_js

## 0.6.1 - 2018-05-22
Beta release
- Using an updated version of dash-renderer-grasia so it uses it instead of the upstream dash-renderer. This uses the Loading component when "updating" the app.

## 0.6.0 - 2018-05-22
Beta release
- Using gdc.Import() to load local js files.
- Added support for standard mediawikis in scripts
- Changed pics
- Added logo
- Better favicon quality
- Improved documentation
- Clean up code

## 0.5.1 - 2018-05-04
Beta release
### Updated
- Updated grasia-dash-components in requirements.txt

## 0.5.0 - 2018-04-25
Beta release
- Added fold button in the sidebar.
- Disabled redis cache in development
- UX improvements
- Retrieving actual number of users in generate_wikis_json.py

## 0.4.0 - 2018-04-13
Beta release
- Some modifications in metrics. Fixing issues.
- Added docs.
- New metrics: edits_in_articles_per_users_monthly and edits_in_articles_per_users_accum
- Added metric descriptions on hover.
- Changed names and order of metrics.
- Added favicon

## 0.3.3 - 2018-03-14
Beta release
### Fixed
- Hot fix for percentage_edits_by_anonymous_accum metric

## 0.3.2 - 2018-03-14
Beta release
### Added
- Added script to generate wikis.json
- Added (Deltas, 2003) correction to Gini computation
- Added metric: Percentage of anonymous edits

## 0.3.1 - 2018-03-07
Beta release
### Added
- Added flask caching for expensive function calls.

## 0.3.0 - 2018-03-06
Beta release
- Important fixes on metric calculations
- Added metric 10:90 ratio
- Customized plotly options for graphs
- Updated dependencies

## 0.2.0 - 2018-02-16
Beta release
### Added
Added metrics to measure distribution and concentration of work. In particular:
- Gini coefficient
- Ratio between the top contributor and different percentile contributor:
  * percentile 20
  * percentile 10
  * percentile 5

## 0.1.4 - 2018-02-13
Beta release
- Changed html title of the webapp to Wikichron
- Changed categories names of big wikis to "Large" and "Very Large"
- Small improvements in deploy.sh shell script

## 0.1.3 - 2018-02-12
Beta release
- scripts/query_bot_users.py now prepend http:// if missing
- Using warnins.warn for some messages.

## 0.1.2 - 2018-02-09
Beta release
- Available wikis are now grouped into collapasable lists depending on its page number
- Added wikis.json file with metadata of shown wikis
- Removed bot activity
- Some minor UI improvements

## 0.1.1 - 2018-02-01
Beta release

## 0.1.0 - 2018-01-29
Beta release

## 0.0.6 - 2017-12-18
Alpha release

## 0.0.5 - 2017-12-13
Alpha release

## 0.0.4 - 2017-12-01
Alpha release

## 0.0.3 - 2017-11-24
Alpha release
### Added
- Added switch absolute - relative datetime axis
- Added environment DEBUG flag

## 0.0.2 - 2017-11-24
Alpha release

## 0.0.1 - 2017-11-22
Alpha release
