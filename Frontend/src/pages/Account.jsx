import { useState, useEffect } from 'react';

import AccountForm from '../components/forms/Account';
import Alert, { DefaultAlert } from '../components/Alert';
import Preloader from '../components/Preloader';
import ProfileTitle from '../layout/ProfileTitle';
import getUserProfile from '../js/api/getUserProfile';
import logOutRequest from '../js/api/logOut';

export default function Account() {
  const [profile, setProfile] = useState({});
  const [alert, setAlert] = useState(DefaultAlert);

  // Effect to load profile data
  useEffect(() => {
    getUserProfile().then((data) => {
      if (data.detail !== undefined) {
        logOutRequest();
      } else {
        const { username, email, first_name, last_name } = data;
        setProfile({
          username: username,
          email: email,
          firstname: first_name,
          lastname: last_name,
        });
      }
    });
  }, []);

  return (
    <>
      {!Object.keys(profile).length ? (
        <Preloader />
      ) : (
        <div className='container'>
          {alert.isVisible ? <Alert alert={alert} setAlert={setAlert} /> : null}
          <ProfileTitle title='Account' />
          <AccountForm
            profile={profile}
            setProfile={setProfile}
            setAlert={setAlert}
          />
        </div>
      )}
    </>
  );
}
