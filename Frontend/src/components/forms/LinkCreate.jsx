import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import $ from 'jquery';

import '../../css/components/controlPanel.css';

import LinkForm from '../../layout/LinkForm';
import { BackendError } from '../../js/enum/errors';
import createLinkRequest from '../../js/api/createLink';
import logOutRequest from '../../js/api/logOut';
import normalizeFormFields from '../../js/processing/normalizer';
import validateLinkForm from '../../js/validation/manageLink';
import { showAlert } from '../Alert';
import {
  showInvalidFields,
  hideInvalidFields,
  removeInvalidFieldStyle,
} from '../../js/style/invalidFormFields';

export default function LinkCreateForm(props) {
  const { defaultValue, setAlert = Function.prototype } = props;
  const [error, setError] = useState(null);
  const [tags, setTags] = useState(defaultValue.tags);
  const navigate = useNavigate();
  const btnId = 'btn-create';

  const setDefaultValues = () => {
    $('#link-title').val('');
    $('#link-url').val('');
    $('#link-annotation').val('');
  };

  const createLink = async () => {
    normalizeFormFields('link-title', 'link-url', 'link-annotation');
    const form = document.getElementById('link-form');
    const [formFields, error] = validateLinkForm(form);
    formFields['tags'] = !tags.length ? null : tags;
    setError(error);
    if (!error) {
      $(`#${btnId}`).prop('disabled', true);
      hideInvalidFields(form);
      const requestBody = JSON.stringify(formFields);
      await createLinkRequest(requestBody).then((data) => {
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
      <div className='col-12 col-xl-6 col-lg-8 col-md-10'>
        <div className='d-flex justify-content-start align-items-center content-control-panel mb-3'>
          <div className='btn-back' onClick={() => navigate(-1)}>
            <i className='icon-arrow-left'></i>Back
          </div>
        </div>
        <LinkForm
          useControlPanel={false}
          btnId={btnId}
          btnName='Create'
          onClick={createLink}
          tags={tags}
          setTags={setTags}
          title={defaultValue.title}
          url={defaultValue.url}
          annotation={defaultValue.annotation}
        />
      </div>
    </div>
  );
}
