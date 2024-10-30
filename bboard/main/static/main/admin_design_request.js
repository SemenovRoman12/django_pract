document.addEventListener("DOMContentLoaded", function() {
    const statusField = document.getElementById("id_status");
    const imageField = document.getElementById("id_design_image").closest(".form-row");
    const commentField = document.getElementById('id_comment');

    function toggleImageField() {
        switch (statusField.value) {
            case "in_progress":
                imageField.style.display = "none";
                commentField.style.display = "";
                break;

            case "completed":
                commentField.style.display = "none";
                imageField.style.display = "";
                break;

            default:
                commentField.style.display = "none";
                imageField.style.display = "none";
                break;
        }

    }

    toggleImageField();
    statusField.addEventListener("change", toggleImageField);
});

