import { useState, useLayoutEffect } from 'react';
import { Navigate, useLocation } from 'react-router-dom';

import Footer from './Footer';
import Header from './Header';
import Preloader from './Preloader';
import verifyUserRequest from '../js/api/verifyUser';

export default function ProtectedPage(component) {
  return <RequireAuth>{component}</RequireAuth>;
}

function RequireAuth({ children }) {
  const [verified, setIsVerified] = useState(null);
  const location = useLocation();

  // Effect to verify user
  useLayoutEffect(() => {
    verifyUserRequest().then((response) => {
      setIsVerified(response.status === 202);
    });
  }, [location.pathname]);

  return verified === null ? (
    <Preloader />
  ) : verified ? (
    <>
      <Header />
      <div className='body-size pt-5'>{children}</div>
      <Footer />
    </>
  ) : (
    <Navigate to={'/'} />
  );
}
