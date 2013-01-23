basePath = '../';

files = [
  JASMINE,
  JASMINE_ADAPTER,
  'static/js/vendor/*.js',
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
