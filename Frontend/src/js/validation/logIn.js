import { FrontendError } from '../enum/errors';
import { setInvalidFieldStyle } from '../style/invalidFormFields';

export default function validateLogInForm(form) {
  const { username, password } = form;
  let error = null;

  [username, password].forEach((field) => {
    if (!field.value) {
      setInvalidFieldStyle(field);
      error = FrontendError.emptyField;
    }
  });

  return [
    {
      'username': username.value,
      'password': password.value
    },
    error
  ];
}