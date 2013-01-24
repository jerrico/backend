describe('directives', function() {
  beforeEach(module('console.services'));

  describe('tw-modal', function() {
    var $compile, scope;

    beforeEach(inject(function(_$compile_, $rootScope) {
      $compile = _$compile_;
      scope = $rootScope.$new();
    }));

    it('adds a few helpers and wrappers', function() {
        spyOn($.fn, 'modal').andCallThrough();
        var element = $compile('<div tw-modal="1"></div>')(scope);
        expect($.fn.modal).toHaveBeenCalledWith("hide");
        expect(scope.show).toBeDefined();
        expect(scope.dismiss).toBeDefined();

        // we simply rely on the tw-bootstrap implementation here
        scope.show();
        expect($.fn.modal).toHaveBeenCalledWith("show");
        scope.dismiss();
        expect($.fn.modal).toHaveBeenCalledWith("hide");
        scope.show();
        expect($.fn.modal).toHaveBeenCalledWith("show");

    });
  });
});
