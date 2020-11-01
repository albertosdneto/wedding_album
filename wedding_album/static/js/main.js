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
            console.log('success');
        });

        return false;
    });

    // Like or remove like from photo
    $('a.like').bind('click', function () {
        var photo_id = $(this).closest('div.card').find('input[name="photo_id"]').val();
        console.log(photo_id)
        $.getJSON('_like', {
            photo_id: photo_id,
        }, function (data) {
            if(data.result == 'liked'){
                $("#liked_" + photo_id).html("<i class=\"fas fa-lg fa-heart\" style=\"color: red\"></i>")
                // $("#liked_" + photo_id).text('<i class="fas fa-lg fa-heart" style="color: red"></i>');
            } else {
                $("#liked_" + photo_id).html("<i class=\"far fa-lg fa-heart\" style=\"color: red\"></i>")
            }


            console.log('like success')
        });
        return false;
    });
});