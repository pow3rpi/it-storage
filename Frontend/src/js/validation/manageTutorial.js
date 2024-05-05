import { Config } from '../../config';
import { FrontendError } from '../enum/errors';
import { setInvalidFieldStyle } from '../style/invalidFormFields';

export default function validateTutorialForm(form) {
  const { title, file } = form;
  const fileSize = new Blob([file.value]).size;
  let error = null;

  if (fileSize > Config.MAX_TUTORIAL_SIZE) {
    setInvalidFieldStyle(file);
    error = FrontendError.fileTooLarge;
  }
  [title, file].forEach((field) => {
    if (!field.value) {
      setInvalidFieldStyle(field);
      error = FrontendError.emptyField;
    }
  });

  return [
    {
      'title': title.value,
      'file': file.value,
      'tags': null
    },
    error
  ];
}