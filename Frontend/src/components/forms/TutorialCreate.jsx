import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import $ from 'jquery';

import '../../css/components/controlPanel.css';

import TutorialForm from '../../layout/TutorialForm';
import { BackendError } from '../../js/enum/errors';
import createTutorialRequest from '../../js/api/createTutorial';
import logOutRequest from '../../js/api/logOut';
import normalizeFormFields from '../../js/processing/normalizer';
import validateTutorialForm from '../../js/validation/manageTutorial';
import { showAlert } from '../Alert';
import {
  showInvalidFields,
  hideInvalidFields,
  removeInvalidFieldStyle,
} from '../../js/style/invalidFormFields';

export default function TutorialCreateForm(props) {
  const { defaultValue, setAlert = Function.prototype } = props;
  const [error, setError] = useState(null);
  const [tutorial, setTutorial] = useState(defaultValue);
  const [tags, setTags] = useState(defaultValue.tags);
  const navigate = useNavigate();
  const btnId = 'btn-create';

  const setDefaultValues = () => {
    $('#tutorial-title').val('');
  };

  const createTutorial = async () => {
    normalizeFormFields('tutorial-title');
    const form = document.getElementById('tutorial-form');
    const [formFields, error] = validateTutorialForm(form);
    formFields['tags'] = !tags.length ? null : tags;
    setError(error);
    if (!error) {
      $(`#${btnId}`).prop('disabled', true);
      hideInvalidFields(form);
      const requestBody = JSON.stringify(formFields);
      await createTutorialRequest(requestBody).then((data) => {
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
          setDefaultValues();
          setTags(defaultValue.tags);
          setTutorial(defaultValue);
          window.scrollTo({
            top: 0,
            behavior: 'smooth',
          });
        }
      });
      $(`#${btnId}`).prop('disabled', false);
    }
  };

  // Effect to display validation errors
  useEffect(() => {
    const alertBlock = $('#error-alert');
    if (error) {
      alertBlock.text(error);
      alertBlock.removeClass('d-none');
    } else {
      alertBlock.text('');
      alertBlock.addClass('d-none');
    }
  }, [error]);

  // Effect to remove invalid field style on click
  useEffect(() => {
    const fields = $('.form-control');
    const formFields = Array.from(fields);
    formFields.forEach((field) =>
      field.addEventListener('click', () => removeInvalidFieldStyle(field))
    );
  }, []);

  return (
    <div className='row justify-content-center'>
      <div className='col-12'>
        <div className='d-flex justify-content-start align-items-center content-control-panel mb-3'>
          <div className='btn-back' onClick={() => navigate(-1)}>
            <i className='icon-arrow-left'></i>Back
          </div>
        </div>
        <TutorialForm
          useControlPanel={false}
          btnId={btnId}
          btnName='Create'
          onClick={createTutorial}
          tags={tags}
          setTags={setTags}
          tutorial={tutorial}
          setTutorial={setTutorial}
        />
      </div>
    </div>
  );
}
