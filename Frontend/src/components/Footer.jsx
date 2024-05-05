import { Link, useLocation } from 'react-router-dom';

import flag from '../img/language.png';

export default function Footer() {
  const { pathname } = useLocation();

  return (
    <footer>
      <div className='container'>
        <div className='row'>
          <div className='col-12'>
            <nav className='navbar navbar-expand-lg bg-body-tertiary'>
              <div className='container-fluid'>
                <div className='navbar-collapse'>
                  <span className='navbar-text pc-copyright'>
                    Copyright © {new Date().getFullYear()} IT-Storage
                  </span>
                  <ul className='navbar-nav me-auto'>
                    <li className='nav-item'>
                      <Link
                        className={`nav-link footer-first-element ${
                          pathname === '/help_center' ? 'active-page' : ''
                        }`}
                        to='/help_center'
                      >
                        Help center
                      </Link>
                    </li>
                    <li className='nav-item'>
                      <Link
                        className={`nav-link ${
                          pathname === '/terms' ? 'active-page' : ''
                        }`}
                        to='/terms'
                      >
                        Terms
                      </Link>
                    </li>
                    <li className='nav-item'>
                      <Link
                        className={`nav-link ${
                          pathname === '/privacy_policy' ? 'active-page' : ''
                        }`}
                        to='/privacy_policy'
                      >
                        Privacy policy
                      </Link>
                    </li>
                  </ul>
                  <div className='pc-language'>
                    <img className='d-block flag' src={flag} alt='English' />
                    <span className='nav-link language-name'>English</span>
                  </div>
                  <div className='d-flex d-lg-none flex-row justify-content-between'>
                    <span className='navbar-text mobile-copyright'>
                      Copyright © {new Date().getFullYear()} IT-Storage
                    </span>
                    <div className='mobile-language'>
                      <img className='d-block flag' src={flag} alt='English' />
                      <span className='nav-link language-name'>English</span>
                    </div>
                  </div>
                </div>
              </div>
            </nav>
          </div>
        </div>
      </div>
    </footer>
  );
}
