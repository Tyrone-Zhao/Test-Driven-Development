QUnit.test( "errors should be hidden on keypress", function (assert) {
    window.Superlists.initialize();
    $("input[name='text']").trigger("keypress");
    assert.equal($(".has-error").is(":visible"), false);
});

QUnit.test("errors aren't hidden if there is no keypress", function (assert) {
    window.Superlists.initialize();
    assert.equal($(".has-error").is(":visible"), true);
});