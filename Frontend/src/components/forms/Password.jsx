import { useEffect, useState } from 'react';
import $ from 'jquery';

import ProfileNav from '../../layout/ProfileNav';
import { BackendError } from '../../js/enum/errors';
import changePasswordRequest from '../../js/api/changePassword';
import logOutRequest from '../../js/api/logOut';
import validateChangePasswordForm from '../../js/validation/changePassword';
import { showAlert } from '../Alert';
import {
  showInvalidFields,
  hideInvalidFields,
  removeInvalidFieldStyle,
} from '../../js/style/invalidFormFields';

export default function PasswordForm({ setAlert }) {
  const [error, setError] = useState(null);

  const changePassword = async () => {
    const form = document.getElementById('changePassword-form');
    const [formFields, error] = validateChangePasswordForm(form);
    setError(error);
    if (!error) {
      $(`#btn-change`).prop('disabled', true);
      hideInvalidFields(form);
      const requestBody = JSON.stringify(formFields);
      await changePasswordRequest(requestBody).then((data) => {
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
          const fields = $('.form-control');
          Array.from(fields).forEach((field) => {
            field.value = '';
          });
        }
      });
      $(`#btn-change`).prop('disabled', false);
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
    const formFields = Array.from(
      document.getElementsByClassName('form-control')
    );
    formFields.forEach((field) =>
      field.addEventListener('click', () => removeInvalidFieldStyle(field))
    );
  }, []);

  return (
    <div className='row justify-content-between'>
      <ProfileNav activePage='password' />
      <div className='col-12 col-lg-9 col-md-9'>
        <form id='changePassword-form'>
          <div className='row mb-3 align-items-center'>
            <label
              htmlFor='profile-currentPassword'
              className='col-12 col-lg-2 col-md-2 mb-lg-3 mb-sm-1 form-label'
            >
              Current password
            </label>
            <div className='col-12 col-xl-6 col-lg-8 col-md-10'>
              <input
                id='profile-currentPassword'
                className='form-control'
                type='password'
                name='currentPassword'
              />
              <div id='passwordHelpBlock' className='form-text'>
                You must provide your current password in order to change it.
              </div>
            </div>
          </div>
          <div className='row mb-3 align-items-center'>
            <label
              htmlFor='profile-newPassword'
              className='col-12 col-lg-2 col-md-2 mb-lg-0 mb-sm-1 form-label'
            >
              New password
            </label>
            <div className='col-12 col-xl-6 col-lg-8 col-md-10'>
              <input
                id='profile-newPassword'
                className='form-control'
                type='password'
                name='password'
              />
            </div>
          </div>
          <div className='row mb-3 align-items-center'>
            <label
              htmlFor='profile-passwordConfirm'
              className='col-12 col-lg-2 col-md-2 mb-lg-0 mb-sm-1 form-label'
            >
              Confirm password
            </label>
            <div className='col-12 col-xl-6 col-lg-8 col-md-10'>
              <input
                id='profile-passwordConfirm'
                className='form-control'
                type='password'
                name='passwordConfirm'
              />
            </div>
          </div>
          <div className='row mb-3 align-items-center alert-error-profile'>
            <div className='col-12 col-lg-2 col-md-2 mb-lg-0'></div>
            <div
              id='error-alert'
              className='d-none col-12 col-xl-6 col-lg-8 col-md-10 alert alert-danger'
              role='alert'
            ></div>
          </div>
        </form>
        <div className='justify-content-center'>
          <div className='col-12 col-xl-8 col-lg-10 col-md-12'>
            <button
              id='btn-change'
              className='btn btn-primary btn-standard float-end mb-5 me-2'
              type='button'
              onClick={changePassword}
            >
              Change
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
