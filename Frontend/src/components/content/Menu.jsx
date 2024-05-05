import MenuItem from './MenuItem';

export default function Menu({ sections = [] }) {
  return (
    <div className='row justify-content-center mb-5 mb-md-0'>
      {sections.map((el, index) => (
        <MenuItem key={index} {...el} />
      ))}
    </div>
  );
}
