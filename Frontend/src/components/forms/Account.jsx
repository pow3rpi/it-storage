import { useState, useEffect } from 'react';
import $ from 'jquery';

import ProfileNav from '../../layout/ProfileNav';
import { BackendError } from '../../js/enum/errors';
import logOutRequest from '../../js/api/logOut';
import normalizeFormFields from '../../js/processing/normalizer';
import updateProfileRequest from '../../js/api/updateProfile';
import validateUpdateProfileForm from '../../js/validation/updateProfile';
import { showAlert } from '../Alert';
import {
  showInvalidFields,
  hideInvalidFields,
  removeInvalidFieldStyle,
} from '../../js/style/invalidFormFields';

export default function AccountForm(props) {
  const { profile = {}, setProfile, setAlert } = props;
  const [error, setError] = useState(null);
  const [formAvailability, setFormAvailability] = useState(false);

  const setDefaultState = () => {
    const fields = $('.form-control');
    $('#btn-update').addClass('d-none');
    $('#btn-cancel').addClass('d-none');
    $('#btn-edit').removeClass('d-none');
    setFormAvailability(false);
    hideInvalidFields(fields);
  };

  const editForm = () => {
    $('#btn-edit').addClass('d-none');
    $('#btn-update').removeClass('d-none');
    $('#btn-cancel').removeClass('d-none');
    setFormAvailability(true);
  };

  const cancelChange = () => {
    $('#error-alert').addClass('d-none');
    setDefaultState();
    const fields = $('.form-control');
    Array.from(fields).forEach((field) => {
      field.value = field.defaultValue;
    });
    setFormAvailability(false);
  };

  document.onkeydown = function (event) {
    if (event.key === 'Escape' && formAvailability === true) {
      cancelChange();
    }
  };

  const updateProfile = async () => {
    normalizeFormFields(
      'profile-username',
      'profile-email',
      'profile-firstname',
      'profile-lastname'
    );
    const form = document.getElementById('updateAccount-form');
    const [formFields, error] = validateUpdateProfileForm(form);
    setError(error);
    if (!error) {
      $('#btn-update').prop('disabled', true);
      $('#btn-cancel').prop('disabled', true);
      hideInvalidFields(form);
      const requestBody = JSON.stringify(formFields);
      await updateProfileRequest(requestBody).then((data) => {
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
          setProfile({
            username: formFields.username.toLowerCase(),
            email: formFields.email,
            firstname: formFields.firstname,
            lastname: formFields.lastname,
          });
          setDefaultState();
          showAlert(setAlert, false);
        }
      });
      $('#btn-update').prop('disabled', false);
      $('#btn-cancel').prop('disabled', false);
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
    <div className='row justify-content-between'>
      <ProfileNav activePage='account' />
      <div className='col-12 col-lg-9 col-md-9'>
        <form id='updateAccount-form'>
          <div className='row mb-3 align-items-center'>
            <label
              htmlFor='profile-firstname'
              className='col-12 col-lg-2 col-md-2 mb-lg-0 mb-sm-1 form-label'
            >
              Username
            </label>
            <div className='col-12 col-xl-6 col-lg-8 col-md-10'>
              <input
                id='profile-username'
                className='form-control'
                type='text'
                name='username'
                defaultValue={profile.username}
                style={{ textTransform: 'lowercase' }}
                disabled={!formAvailability}
              />
            </div>
          </div>
          <div className='row mb-3 align-items-center'>
            <label
              htmlFor='profile-email'
              className='col-12 col-lg-2 col-md-2 mb-lg-0 mb-sm-1 form-label'
            >
              Email
            </label>
            <div className='col-12 col-xl-6 col-lg-8 col-md-10'>
              <input
                id='profile-email'
                className='form-control'
                type='email'
                name='email'
                defaultValue={profile.email}
                style={{ textTransform: 'lowercase' }}
                disabled={!formAvailability}
              />
            </div>
          </div>
          <div className='row mb-3 align-items-center'>
            <label
              htmlFor='profile-firstname'
              className='col-12 col-lg-2 col-md-2 mb-lg-0 mb-sm-1 form-label'
            >
              First Name
            </label>
            <div className='col-12 col-xl-6 col-lg-8 col-md-10'>
              <input
                id='profile-firstname'
                className='form-control'
                type='text'
                name='firstname'
                defaultValue={profile.firstname}
                disabled={!formAvailability}
              />
            </div>
          </div>
          <div className='row mb-3 align-items-center'>
            <label
              htmlFor='profile-lastname'
              className='col-12 col-lg-2 col-md-2 mb-lg-0 mb-sm-1 form-label'
            >
              Last Name
            </label>
            <div className='col-12 col-xl-6 col-lg-8 col-md-10'>
              <input
                id='profile-lastname'
                className='form-control'
                type='text'
                name='lastname'
                defaultValue={profile.lastname}
                disabled={!formAvailability}
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
              id='btn-edit'
              className='btn btn-primary btn-standard float-end mb-5 me-md-0 me-xl-2 me-lg-1 me-sm-0 me-xs-2'
              type='button'
              onClick={editForm}
            >
              Edit
            </button>
            <button
              id='btn-cancel'
              className='d-none btn btn-outline-primary btn-standard float-end mb-5 me-md-0 me-xl-2 me-lg-1 me-sm-0 me-xs-2'
              type='button'
              onClick={cancelChange}
            >
              Cancel
            </button>
            <button
              id='btn-update'
              className='d-none btn btn-primary btn-standard float-end mb-5 me-2'
              type='button'
              onClick={updateProfile}
            >
              Update
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
