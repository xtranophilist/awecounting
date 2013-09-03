$(document).ready(function () {
    $('.date-picker').datepicker();

    $('#day-journal-selection-button').on('click', function () {
        window.location = '/day/' + $('#day-journal-date').val();
    });
});


