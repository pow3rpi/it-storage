import { FrontendError } from '../enum/errors';
import { setInvalidFieldStyle } from '../style/invalidFormFields';

export default function validateSignUpForm(form) {
  const { username, email, firstname, lastname, password, passwordConfirm } = form;
  let error = null;

  // eslint-disable-next-line
  if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email.value)) {
    setInvalidFieldStyle(email);
    error = FrontendError.invalidEmail;
  }
  [username, password, passwordConfirm].forEach((field) => {
    if (!field.value) {
      setInvalidFieldStyle(field);
      error = FrontendError.emptyField;
    }
  });

  return [
    {
      'username': username.value,
      'email': email.value,
      'first_name': firstname.value,
      'last_name': lastname.value,
      'password': password.value,
      'password_confirm': passwordConfirm.value
    },
    error
  ];
}