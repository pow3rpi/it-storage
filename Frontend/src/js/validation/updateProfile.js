import { FrontendError } from '../enum/errors';
import { setInvalidFieldStyle } from '../style/invalidFormFields';

export default function validateUpdateProfileForm(form) {
  const { username, email, firstname, lastname } = form;
  let error = null;

  // eslint-disable-next-line
  if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email.value)) {
    setInvalidFieldStyle(email);
    error = FrontendError.invalidEmail;
  }
  if (!username.value) {
    setInvalidFieldStyle(username);
    error = FrontendError.emptyField;
  }

  return [
    {
      'username': username.value,
      'email': email.value,
      'first_name': firstname.value,
      'last_name': lastname.value
    },
    error
  ];
}