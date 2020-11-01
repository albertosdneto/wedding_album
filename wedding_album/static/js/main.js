$(function () {
    $('a.role').bind('click', function () {
        var id = $(this).closest('li').find('input[name="id"]').val();
        console.log(id)
        $.getJSON('_change_role', {
            id: id,
        }, function (data) {
            $("#role_" + id).text(data.result);
        });
        return false;
    });
});