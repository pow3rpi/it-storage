import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import $ from 'jquery';

import logInRequest from '../../js/api/logIn';
import normalizeFormFields from '../../js/processing/normalizer';
import signUpRequest from '../../js/api/signUp';
import validateLogInForm from '../../js/validation/logIn';
import validateSignUpForm from '../../js/validation/signUp';
import { BackendError } from '../../js/enum/errors';
import { Config } from '../../config';
import {
  showInvalidFields,
  hideInvalidFields,
  removeInvalidFieldStyle,
} from '../../js/style/invalidFormFields';

export default function AuthForm() {
  const [logInError, setLogInError] = useState(null);
  const [signUpError, setSignUpError] = useState(null);
  const navigate = useNavigate();

  const logIn = async () => {
    const form = document.getElementById('logIn-form');
    const [formFields, error] = validateLogInForm(form);
    setLogInError(error);
    if (!error) {
      $('#btn-logIn').prop('disabled', true);
      hideInvalidFields(form);
      const requestBody = new URLSearchParams(formFields);
      await logInRequest(requestBody).then((data) => {
        const error_code = data.detail;
        if (error_code !== undefined) {
          setLogInError(BackendError[error_code].text);
          showInvalidFields(form, error_code);
        } else {
          navigate('/profile');
        }
      });
      $(`#btn-logIn`).prop('disabled', false);
    }
  };

  const signUp = async () => {
    normalizeFormFields(
      'signUp-username',
      'signUp-email',
      'signUp-firstname',
      'signUp-lastname'
    );
    const form = document.getElementById('signUp-form');
    const [formFields, error] = validateSignUpForm(form);
    setSignUpError(error);
    if (!error) {
      $('#btn-signUp').prop('disabled', true);
      hideInvalidFields(form);
      const requestBody = JSON.stringify(formFields);
      await signUpRequest(requestBody).then((data) => {
        const error_code = data.detail;
        if (error_code !== undefined) {
          setSignUpError(BackendError[error_code].text);
          showInvalidFields(form, error_code);
        } else {
          navigate('/email_verification');
        }
      });
      $('#btn-signUp').prop('disabled', false);
    }
  };

  // Effect to display validation errors for logIn
  useEffect(() => {
    const alertBlock = $('#logIn-error');
    if (logInError) {
      alertBlock.text(logInError);
      alertBlock.removeClass('d-none');
    } else {
      alertBlock.text('');
      alertBlock.addClass('d-none');
    }
  }, [logInError]);

  // Effect to display validation errors for signUp
  useEffect(() => {
    const alertBlock = $('#signUp-error');
    if (signUpError) {
      alertBlock.text(signUpError);
      alertBlock.removeClass('d-none');
    } else {
      alertBlock.text('');
      alertBlock.addClass('d-none');
    }
  }, [signUpError]);

  // Effect to remove invalid field style on click
  useEffect(() => {
    const formFields = Array.from($('.form-control'));
    formFields.forEach((field) =>
      field.addEventListener('click', () => removeInvalidFieldStyle(field))
    );
  }, []);

  return (
    <div className='row justify-content-center'>
      <div className='col-12 col-lg-4 col-md-8 mb-3'>
        <nav>
          <div className='nav nav-tabs mb-3' id='nav-tab' role='tablist'>
            <button
              id='nav-logIn-tab'
              className='nav-link active'
              data-bs-toggle='tab'
              data-bs-target='#nav-logIn'
              type='button'
              role='tab'
              aria-controls='nav-logIn'
              aria-selected='true'
            >
              Log In
            </button>
            <button
              id='nav-signUp-tab'
              className='nav-link'
              data-bs-toggle='tab'
              data-bs-target='#nav-signUp'
              type='button'
              role='tab'
              aria-controls='nav-signUp'
              aria-selected='false'
            >
              Sign Up
            </button>
          </div>
        </nav>
        <div className='tab-content' id='nav-tabContent'>
          <div
            id='nav-logIn'
            className='tab-pane fade show active'
            role='tabpanel'
            aria-labelledby='nav-logIn-tab'
            tabIndex='0'
          >
            <form id='logIn-form'>
              <div className='mb-3'>
                <label htmlFor='logIn-username' className='form-label'>
                  Username <span className='required-field'>*</span>
                </label>
                <input
                  id='logIn-username'
                  className='form-control'
                  type='text'
                  name='username'
                  style={{ textTransform: 'lowercase' }}
                  required
                />
              </div>
              <div className='mb-3'>
                <label htmlFor='logIn-password' className='form-label'>
                  Password <span className='required-field'>*</span>
                </label>
                <input
                  id='logIn-password'
                  className='form-control'
                  type='password'
                  name='password'
                  required
                />
              </div>
              <div
                id='logIn-error'
                className='d-none alert alert-danger mb-3'
                role='alert'
              ></div>
              <button
                id='btn-logIn'
                className='btn btn-primary btn-standard float-end mb-5'
                type='button'
                onClick={logIn}
              >
                Log In
              </button>
            </form>
          </div>
          <div
            id='nav-signUp'
            className='tab-pane fade'
            role='tabpanel'
            aria-labelledby='nav-signUp-tab'
            tabIndex='0'
          >
            <form id='signUp-form'>
              <div className='mb-3'>
                <label htmlFor='signUp-username' className='form-label'>
                  Username <span className='required-field'>*</span>
                </label>
                <input
                  id='signUp-username'
                  className='form-control'
                  type='text'
                  name='username'
                  style={{ textTransform: 'lowercase' }}
                  required
                />
              </div>
              <div className='mb-3'>
                <label htmlFor='signUp-email' className='form-label'>
                  Email <span className='required-field'>*</span>
                </label>
                <input
                  id='signUp-email'
                  className='form-control'
                  type='email'
                  name='email'
                  placeholder='name@example.com'
                  style={{ textTransform: 'lowercase' }}
                  required
                />
              </div>
              <div className='mb-3'>
                <label htmlFor='signUp-firstname' className='form-label'>
                  First Name
                </label>
                <input
                  id='signUp-firstname'
                  className='form-control'
                  type='text'
                  name='firstname'
                />
              </div>
              <div className='mb-3'>
                <label htmlFor='signUp-lastname' className='form-label'>
                  Last Name
                </label>
                <input
                  id='signUp-lastname'
                  className='form-control'
                  type='text'
                  name='lastname'
                />
              </div>
              <div className='mb-3'>
                <label htmlFor='signUp-password' className='form-label'>
                  Password <span className='required-field'>*</span>
                </label>
                <input
                  id='signUp-password'
                  className='form-control'
                  type='password'
                  name='password'
                  required
                />
                <div id='passwordHelpBlock' className='form-text'>
                  Your password must be {Config.MIN_PWD_LENGTH}-
                  {Config.MAX_PWD_LENGTH} characters long, contain letters in
                  both cases, numbers and special characters, and must not
                  contain spaces or emoji.
                </div>
              </div>
              <div className='mb-3'>
                <label htmlFor='signUp-passwordConfirm' className='form-label'>
                  Confirm Password <span className='required-field'>*</span>
                </label>
                <input
                  id='signUp-passwordConfirm'
                  className='form-control'
                  type='password'
                  name='passwordConfirm'
                  required
                />
              </div>
              <div
                id='signUp-error'
                className='d-none alert alert-danger mb-3'
                role='alert'
              ></div>
              <button
                id='btn-signUp'
                className='btn btn-primary btn-standard float-end mb-5'
                type='button'
                onClick={signUp}
              >
                Sign Up
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
