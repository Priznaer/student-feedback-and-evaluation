const student_fields = document.getElementsByClassName('student')
const non_student_fields = document.getElementsByClassName('non-student')

function add_radio_listener() {
    document.getElementById("student").addEventListener("click", () => filter_form("student"))
    document.getElementById("lecturer").addEventListener("click", () => filter_form("lecturer"))
    document.getElementById("admin").addEventListener("click", () => filter_form("admin"))
}
add_radio_listener();
document.getElementById("student").click();


function filter_form(element_id) {

    // Showing student fields and hidding non-student fields
    if (element_id == "student") {
        for (let idx=0; idx<student_fields.length; idx++) {
            let element = student_fields[idx];
            if (element.hasAttribute('hidden')) {
                element.removeAttribute('hidden');
                element.setAttribute('required', '');
            }
        }
        for (let idx=0; idx<non_student_fields.length; idx++) {
            let element = non_student_fields[idx];
            if (!element.hasAttribute('hidden')) {
                element.setAttribute('hidden', '');
                element.removeAttribute('required');
            }
        }
    }
    // Showing non-student fields and hidding student fields
    else {
        for (let idx=0; idx<non_student_fields.length; idx++) {
            let element = non_student_fields[idx];
            if (element.hasAttribute('hidden')) {
                element.removeAttribute('hidden');
                element.setAttribute('required', '');
            }
        }
        for (let idx=0; idx<student_fields.length; idx++) {
            let element = student_fields[idx];
            if (!element.hasAttribute('hidden')) {
                element.setAttribute('hidden', '');
                element.removeAttribute('required');
            }
        }
    }
}