# Elasticsearch Integration for XL Release

[![Build Status](https://travis-ci.org/xebialabs-community/xlr-elasticsearch-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-elasticsearch-plugin)
![GitHub release](https://img.shields.io/github/release/xebialabs-community/xlr-elasticsearch-plugin.svg)
[![License: MIT][xlr-elasticsearch-plugin-license-image]][xlr-elasticsearch-plugin-license-url]
[![Github All Releases][xlr-elasticsearch-plugin-downloads-image]][xlr-elasticsearch-plugin-releases-url]
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-blue.svg)](https://github.com/RichardLitt/standard-readme)

> The Elasticsearch plugin enables elastic stack monitoring in XL Release

## Installation

### Requirements

1. XL Release 9.0+

### Building the plugin
The gradle wrapper facilitates building the plugin.  Use the following command to build using [Gradle](https://gradle.org/):
```bash
./gradlew clean build
```
The built plugin, along with other files from the build, can then be found in the _build_ folder.

### Adding the plugin to XL Release

Download the latest version of the plugin from the [releases page][xlr-elasticsearch-plugin-releases-url].  The plugin can then be installed through the XL Release graphical interface or the server backend.  For additional detail, please refer to [the docs.xebialabs.com documentation on XLR plugin installation](https://docs.xebialabs.com/xl-release/how-to/install-or-remove-xl-release-plugins.html)

### Configuration

The Elasticsearch server can be configured at a global level, in _Shared Configuration_, or on a finer lever (e.g. at the folder level).  Please refer to [the docs.xebialabs.com documentation on configurations](https://docs.xebialabs.com/xl-release/how-to/create-custom-configuration-types.html#configuration-page).

## Usage

### Tasks

#### Check Hits
Properties:
* Server _input_ 
* Username _input_ 
   * Optionally, override the username used to connect to the server
* Password _input_ 
   * Optionally, override the password used to connect to the server
* Index _input_ 
   * Elasticsearch index
* Query _input_ 
   * Optionally, provide a query using the Lucene query string syntax
* Time Period _input_ 
   * The number of seconds to inspect hit response codes
* Acceptable 1xx Percent _input_ 
   * The maximum permissible percentage of responses with http status code in the range 100-199.  For no limit, use a value of -1.
* Acceptable 2xx Percent _input_ 
   * The maximum permissible percentage of responses with http status code in the range 200-299.  For no limit, use a value of -1.
* Acceptable 3xx Percent _input_ 
   * The maximum permissible percentage of responses with http status code in the range 300-399.  For no limit, use a value of -1.
* Acceptable 4xx Percent _input_ 
   * The maximum permissible percentage of responses with http status code in the range 400-499.  For no limit, use a value of -1.
* Acceptable 5xx Percent _input_ 
   * The maximum permissible percentage of responses with http status code in the range 500-599.  For no limit, use a value of -1.
* Timestamp Field _input_ 
   * The name of the field for the timestamp
* Response Field _input_ 
   * The name of the field for the HTTP response status code

## Contributing

Please review the contributing guidelines for _xebialabs-community_ at [http://xebialabs-community.github.io/](http://xebialabs-community.github.io/)

## License

This community plugin is licensed under the [MIT license][xlr-elasticsearch-plugin-license-url].

See license in [LICENSE.md](LICENSE.md)

[xlr-elasticsearch-plugin-license-image]: https://img.shields.io/badge/license-MIT-yellow.svg
[xlr-elasticsearch-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-elasticsearch-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-elasticsearch-plugin/total.svg
[xlr-elasticsearch-plugin-releases-url]: https://github.com/xebialabs-community/xlr-elasticsearch-plugin/releases
