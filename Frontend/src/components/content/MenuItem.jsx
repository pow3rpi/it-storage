import { Link } from 'react-router-dom';

import '../../css/components/menuItem.css';

export default function MenuItem({ name, subdomain, pic, description = '' }) {
  return (
    <div className='col-10 col-md-6 me-md-4 ms-md-4 mb-5 mb-md-0 d-flex flex-column text-center content-item'>
      <Link to={`/manage_content/${subdomain}`} className='content-item-link'>
        <div className='mb-2' style={{ color: '#212529' }}>
          <i className={`${pic} me-md-2`}></i>
          {name}
        </div>
        <div className='content-item-description'>{description}</div>
      </Link>
    </div>
  );
}
