basePath = '../';

files = [
  JASMINE,
  JASMINE_ADAPTER,
  'static/js/vendor/jquery*.js',
  'static/js/vendor/bootstrap.min.js',
  'static/js/vendor/angular.min.js',
  'static/js/vendor/angular-resource.min.js',
  'static/js/vendor/angular-ui.min.js',
  'test/lib/angular/angular-mocks.js',
  'static/js/*.js',
  'test/unit/**/*.js'
];

autoWatch = true;

browsers = ['Chrome'];

junitReporter = {
  outputFile: 'test_out/unit.xml',
  suite: 'unit'
};
