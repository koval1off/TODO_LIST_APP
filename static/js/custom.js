$(document).ready(function() {
    $("task-form").on("submit", function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function(data) {
                $("task-list").load(location.href + " #task-list>*", "");
                $("task-form")[0].reset();
            }
        });
    });
});
