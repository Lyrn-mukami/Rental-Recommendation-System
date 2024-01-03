var form_fields = document.querySelectorAll('[id^="id_"]')
form_fields[0].placeholder = 'Username..';
form_fields[1].placeholder = 'Email..';
form_fields[2].placeholder = 'Enter password..';
form_fields[3].placeholder = 'Re-enter password..';

for (var field in form_fields) {
  form_fields[field].className += 'input'
}