import { useState } from 'react';

export default function ProfileTitle({ title }) {
  const [profileTitle, setProfileTitle] = useState(title);

  window.onresize = () => {
    setProfileTitle(window.screen.width >= 768 ? title : 'Profile');
  };

  return (
    <div className='row'>
      <div className='col-12'>
        <h2 className='text-center mb-5 mt-5'>
          {window.screen.width < 768 ? 'Profile' : profileTitle}
        </h2>
      </div>
    </div>
  );
}
