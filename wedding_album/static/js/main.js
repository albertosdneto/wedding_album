$(function () {
    // Change user role
    $('a.role').bind('click', function () {
        var id = $(this).closest('li').find('input[name="id"]').val();
        $.getJSON('_change_role', {
            id: id,
        }, function (data) {
            $("#role_" + id).text(data.result);
        });
        return false;
    });

    // Shows or hide photo
    $("input[type='checkbox']").change(function () {
        var id = $(this).attr('id');
        var status = 'False';
        if (this.checked) {
            console.log('True')
            status = 'True';
        } else {
            status = 'False';
        }

        $.getJSON('_change_visibility', {
            id: id,
            status: status,
        }, function (data) {
            // $("#role_" + id).text(data.result);
            console.log('success');
        });

        return false;
    });
});