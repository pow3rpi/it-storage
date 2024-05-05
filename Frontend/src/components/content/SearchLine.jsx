import '../../css/components/search.css';

export default function SearchLine(props) {
  const { searchFilter, setSearchFilter, onSearch } = props;

  const handleKey = (event) => {
    if (event.key === 'Enter') onSearch();
  };

  return (
    <div className='input-group'>
      <input
        type='text'
        className='form-control search-line'
        placeholder='Search by name'
        aria-describedby='search-btn'
        onKeyDown={handleKey}
        onChange={(event) => {
          setSearchFilter((state) => ({
            ...state,
            searchValue: event.target.value,
          }));
        }}
        defaultValue={searchFilter.searchValue}
      />
      <span
        id='search-btn'
        className='input-group-text btn-search'
        onClick={onSearch}
      >
        <i className='icon-search'></i>
      </span>
    </div>
  );
}
