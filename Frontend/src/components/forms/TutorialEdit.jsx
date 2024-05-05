import { useEffect, useState } from 'react';
import $ from 'jquery';

import ControlPanel from '../content/PanelContent';
import TutorialForm from '../../layout/TutorialForm';
import TutorialPreview from '../../layout/TutorialPreview';
import { BackendError } from '../../js/enum/errors';
import logOutRequest from '../../js/api/logOut';
import normalizeFormFields from '../../js/processing/normalizer';
import updateTutorialRequest from '../../js/api/updateTutorial';
import validateTutorialForm from '../../js/validation/manageTutorial';
import { showAlert } from '../Alert';
import {
  showInvalidFields,
  hideInvalidFields,
  removeInvalidFieldStyle,
} from '../../js/style/invalidFormFields';

export default function TutorialEditForm(props) {
  const { id, tutorial, setTutorial, setAlert } = props;
  const [error, setError] = useState(null);
  const [currentTags, setCurrentTags] = useState(tutorial.tags);
  const [isEdit, setIsEdit] = useState(false);
  const [isWaitingResponse, setIsWaitingResponse] = useState(false);

  const updateTutorial = async () => {
    normalizeFormFields('tutorial-title');
    const form = document.getElementById('tutorial-form');
    const [formFields, error] = validateTutorialForm(form);
    formFields['tags'] = !currentTags.length ? null : currentTags;
    setError(error);
    if (!error) {
      setIsWaitingResponse(true);
      hideInvalidFields(form);
      const requestBody = JSON.stringify(formFields);
      await updateTutorialRequest(id, requestBody).then((data) => {
        const error_code = data.detail;
        if (error_code !== undefined) {
          if (error_code === 12) {
            logOutRequest();
          } else {
            showAlert(setAlert, true);
            setError(BackendError[error_code].text);
            showInvalidFields(form, error_code);
          }
        } else {
          showAlert(setAlert, false);
          setTutorial({
            title: formFields.title,
            tags: formFields.tags ? formFields.tags : [],
            file: formFields.file,
            size: new Blob([formFields.file]).size,
          });
          setIsEdit(false);
        }
      });
      setIsWaitingResponse(false);
    }
  };

  // Effect to display validation errors
  useEffect(() => {
    if (isEdit) {
      const alertBlock = $('#error-alert');
      if (error) {
        alertBlock.text(error);
        alertBlock.removeClass('d-none');
      } else {
        alertBlock.text('');
        alertBlock.addClass('d-none');
      }
    }
  }, [error, isEdit]);

  // Effect to remove invalid field style on click
  useEffect(() => {
    if (isEdit) {
      const fields = $('.form-control');
      const formFields = Array.from(fields);
      formFields.forEach((field) =>
        field.addEventListener('click', () => removeInvalidFieldStyle(field))
      );
    }
  }, [isEdit]);

  return (
    <>
      <div className='row'>
        <h2 className='col-12 text-center mb-5 mt-lg-5'>
          {isEdit ? `Edit Tutorial #${id}` : `Tutorial #${id}`}
        </h2>
      </div>
      <div className='row justify-content-center'>
        <div className='col-12'>
          <ControlPanel
            id={id}
            setAlert={setAlert}
            isEdit={isEdit}
            onEdit={() => setIsEdit(true)}
            onCancel={() => setIsEdit(false)}
            onAccept={updateTutorial}
            isWaitingResponse={isWaitingResponse}
          />
          {isEdit ? (
            <TutorialForm
              tags={currentTags}
              setTags={setCurrentTags}
              tutorial={tutorial}
              setTutorial={setTutorial}
            />
          ) : (
            <TutorialPreview
              title={tutorial.title}
              tags={tutorial.tags}
              file={tutorial.file}
              size={tutorial.size}
            />
          )}
        </div>
      </div>
    </>
  );
}
