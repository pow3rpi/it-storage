import { FrontendError } from '../enum/errors';
import { setInvalidFieldStyle } from '../style/invalidFormFields';

export default function validateChangePasswordForm(form) {
  const { currentPassword, password, passwordConfirm } = form;
  let error = null;

  [currentPassword, password, passwordConfirm].forEach((field) => {
    if (!field.value) {
      setInvalidFieldStyle(field);
      error = FrontendError.emptyField;
    }
  });

  return [
    {
      'current_password': currentPassword.value,
      'password': password.value,
      'password_confirm': passwordConfirm.value
    },
    error
  ];
}