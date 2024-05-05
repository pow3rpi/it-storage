import { BackendError } from '../enum/errors';

function setInvalidFieldStyle(field) {
  field.style.boxShadow = '0 0 0 .25rem #f1aeb5';
  field.style.borderColor = '#f1aeb5';
};

function showInvalidFields(form, error_code) {
  Array.from(form).forEach((field) => {
    if (BackendError[error_code].field.includes(field.name) && field.role !== 'tab') {
      setInvalidFieldStyle(field);
    }
  });
};

function removeInvalidFieldStyle(field) {
  field.style.boxShadow = '';
  field.style.borderColor = '#ced4da';
};

function hideInvalidFields(form) {
  Array.from(form).forEach((field) => {
    if (field.role !== 'tab') removeInvalidFieldStyle(field);
  });
}

export { setInvalidFieldStyle, showInvalidFields, removeInvalidFieldStyle, hideInvalidFields };