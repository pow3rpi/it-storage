import { useEffect, useState } from 'react';
import $ from 'jquery';

import ControlPanel from '../content/PanelContent';
import LinkForm from '../../layout/LinkForm';
import LinkPreview from '../../layout/LinkPreview';
import { BackendError } from '../../js/enum/errors';
import logOutRequest from '../../js/api/logOut';
import normalizeFormFields from '../../js/processing/normalizer';
import updateLinkRequest from '../../js/api/updateLink';
import validateLinkForm from '../../js/validation/manageLink';
import { showAlert } from '../Alert';
import {
  showInvalidFields,
  hideInvalidFields,
  removeInvalidFieldStyle,
} from '../../js/style/invalidFormFields';

export default function LinkEditForm(props) {
  const { id, link, setLink, setAlert } = props;
  const [error, setError] = useState(null);
  const [currentTags, setCurrentTags] = useState(link.tags);
  const [isEdit, setIsEdit] = useState(false);
  const [isWaitingResponse, setIsWaitingResponse] = useState(false);

  const updateLink = async () => {
    normalizeFormFields('link-title', 'link-url', 'link-annotation');
    const form = document.getElementById('link-form');
    const [formFields, error] = validateLinkForm(form);
    formFields['tags'] = !currentTags.length ? null : currentTags;
    setError(error);
    if (!error) {
      setIsWaitingResponse(true);
      hideInvalidFields(form);
      const requestBody = JSON.stringify(formFields);
      await updateLinkRequest(id, requestBody).then((data) => {
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
          setLink({
            title: formFields.title,
            tags: formFields.tags ? formFields.tags : [],
            url: formFields.url,
            annotation: formFields.annotation,
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
          {isEdit ? `Edit Link #${id}` : `Link #${id}`}
        </h2>
      </div>
      <div className='row justify-content-center'>
        <div className='col-12 col-xl-6 col-lg-8 col-md-10 mb-5'>
          <ControlPanel
            id={id}
            setAlert={setAlert}
            isEdit={isEdit}
            onEdit={() => setIsEdit(true)}
            onCancel={() => setIsEdit(false)}
            onAccept={updateLink}
            isWaitingResponse={isWaitingResponse}
          />
          {isEdit ? (
            <LinkForm
              tags={currentTags}
              setTags={setCurrentTags}
              title={link.title}
              url={link.url}
              annotation={link.annotation}
            />
          ) : (
            <LinkPreview
              title={link.title}
              tags={link.tags}
              url={link.url}
              annotation={link.annotation}
            />
          )}
        </div>
      </div>
    </>
  );
}
