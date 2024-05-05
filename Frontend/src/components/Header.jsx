import { Link, useLocation } from 'react-router-dom';

import logOutRequest from '../js/api/logOut';

import logo from '../img/logo.png';

export default function Header() {
  const { pathname } = useLocation();

  return (
    <header>
      <div className='container'>
        <div className='row'>
          <div className='col-12'>
            <nav className='navbar navbar-expand-lg bg-body-tertiary'>
              <div className='container-fluid'>
                <Link className='navbar-brand' to='/search'>
                  <img
                    className='d-inline-block logo'
                    src={logo}
                    alt='IT-Storage'
                  />{' '}
                  <span className='d-inline-block project-name'>
                    IT-Storage
                  </span>
                </Link>
                <button
                  className='navbar-toggler'
                  type='button'
                  data-bs-toggle='collapse'
                  data-bs-target='#navbarNavDropdown'
                  aria-controls='navbarNavDropdown'
                  aria-expanded='false'
                  aria-label='Toggle navigation'
                >
                  <span className='navbar-toggler-icon'></span>
                </button>
                <div
                  className='collapse navbar-collapse'
                  id='navbarNavDropdown'
                >
                  <ul className='navbar-nav me-auto'>
                    <li className='nav-item'>
                      <Link
                        className={`nav-link ${
                          pathname === '/search' ? 'active-page' : ''
                        }`}
                        to='/search'
                      >
                        Search
                      </Link>
                    </li>
                    <li className='nav-item'>
                      <Link
                        className={`nav-link ${
                          pathname === '/manage_content' ? 'active-page' : ''
                        }`}
                        to='/manage_content'
                      >
                        Manage content
                      </Link>
                    </li>
                    <li className='nav-item'>
                      <Link
                        className={`nav-link ${
                          pathname.startsWith('/profile') ? 'active-page' : ''
                        }`}
                        to='/profile'
                      >
                        Profile
                      </Link>
                    </li>
                  </ul>
                  <ul className='navbar-nav'>
                    <li className='nav-item'>
                      <span
                        className='nav-link log-out-pos'
                        onClick={async () => logOutRequest()}
                      >
                        Log-out <i className='icon-logout'></i>
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </nav>
          </div>
        </div>
      </div>
    </header>
  );
}
