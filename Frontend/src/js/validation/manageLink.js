import { FrontendError } from '../enum/errors';
import { setInvalidFieldStyle } from '../style/invalidFormFields';

export default function validateLinkForm(form) {
  const { title, url, annotation } = form;
  let error = null;

  try {
    new URL(url.value);
  } catch (_) {
    setInvalidFieldStyle(url);
    error = FrontendError.invalidUrl;
  }
  [title, url].forEach((field) => {
    if (!field.value) {
      setInvalidFieldStyle(field);
      error = FrontendError.emptyField;
    }
  });

  return [
    {
      'title': title.value,
      'url': url.value,
      'annotation': annotation.value,
    },
    error
  ];
}