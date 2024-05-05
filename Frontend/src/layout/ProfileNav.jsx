import { Link } from 'react-router-dom';

import '../css/layout/profileNav.css';

export default function ProfileNav({ activePage }) {
  return (
    <div className='col-12 col-lg-2 col-md-2'>
      <div className='d-none d-md-block profile-pc-nav list-group'>
        <Link
          to='/profile/account'
          className={`list-group-item list-group-item-action ${
            activePage === 'account' ? 'active' : ''
          }`}
        >
          Account
        </Link>
        <Link
          to='/profile/password'
          className={`list-group-item list-group-item-action ${
            activePage === 'password' ? 'active' : ''
          }`}
        >
          Password
        </Link>
      </div>
      <div className='d-flex d-md-none justify-content-center mb-4'>
        <Link
          className={`d-block account-mobile-nav col-6 col-col-md-4 ${
            activePage === 'account' ? 'active-section' : ''
          }`}
          to='/profile/account'
        >
          Account
        </Link>
        <Link
          className={`d-block password-mobile-nav col-6 col-md-4 ${
            activePage === 'password' ? 'active-section' : ''
          }`}
          to='/profile/password'
        >
          Password
        </Link>
      </div>
    </div>
  );
}
