export default function Tag(props) {
  const { name, setTags = Function.prototype, removeOption = true } = props;

  const removeTag = () => {
    setTags((oldTags) => oldTags.filter((tag) => tag !== name));
  };

  return (
    <div className='tag d-flex flex-row me-2 mt-2 align-items-center'>
      <div style={removeOption ? { marginRight: '5px' } : null}>{name}</div>
      {removeOption ? (
        <button
          type='button'
          className='btn-close'
          onClick={removeTag}
        ></button>
      ) : null}
    </div>
  );
}
