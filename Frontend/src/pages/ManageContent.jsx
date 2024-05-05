import Menu from '../components/content/Menu';
import { Sections } from '../js/enum/content';

export default function ManageContent() {
  const sections = Object.keys(Sections).map((key) => Sections[key]);

  return (
    <div className='container'>
      <div className='row'>
        <div className='col-12'>
          <h2 className='text-center mb-5 mt-lg-5'>Content Types</h2>
        </div>
      </div>
      <Menu sections={sections} />
    </div>
  );
}
