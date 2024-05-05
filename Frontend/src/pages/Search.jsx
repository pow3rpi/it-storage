import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

import ControlPanel from '../components/content/PanelSearch';
import SearchLine from '../components/content/SearchLine';
import SearchList from '../components/content/SearchList';
import TagSection from '../components/tags/TagSection';
import { PreloaderSearch, PreloaderNextPage } from '../components/Preloader';
import { SearchType, SearchBy } from '../js/enum/search';
import getPostsRequest from '../js/api/getPosts';
import logOutRequest from '../js/api/logOut';

export default function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchFilter, setSearchFilter] = useState({
    page: 0,
    type: searchParams.get('type') ? searchParams.get('type') : SearchType.all,
    searchBy: searchParams.get(SearchBy.topic) ? SearchBy.topic : SearchBy.name,
    searchValue: searchParams.get(SearchBy.name)
      ? searchParams.get(SearchBy.name)
      : '',
  });
  const [tags, setTags] = useState(
    searchParams.get(SearchBy.topic) ? searchParams.getAll(SearchBy.topic) : []
  );
  const [posts, setPosts] = useState([]);
  const [total, setTotal] = useState(0);
  const [isMore, setIsMore] = useState(false);
  const [isFound, setIsFound] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handlePosts = async () => {
    switch (true) {
      case searchFilter.searchBy === SearchBy.name:
        setSearchParams({
          type: searchFilter.type,
          name: searchFilter.searchValue,
        });
        break;
      case searchFilter.searchBy === SearchBy.topic:
        setSearchParams({
          type: searchFilter.type,
          topic: tags,
        });
        break;
      default:
        break;
    }
  };

  const loadNextPage = async () => {
    setIsLoading(true);
    const params = { type: searchFilter.type, page: searchFilter.page };
    if (tags.length > 0) params.topic = tags;
    if (searchFilter.searchValue) params.name = searchFilter.searchValue;
    await getPostsRequest(params).then((data) => {
      const error_code = data.detail;
      if (error_code !== undefined) {
        if (error_code === 12) logOutRequest();
      } else {
        setIsLoading(false);
        if (posts.length + data.posts.length === total) setIsMore(false);
        setPosts((oldPosts) => [...oldPosts, ...data.posts]);
        setSearchFilter((state) => ({ ...state, page: state.page + 1 }));
      }
    });
  };

  // Effect for posts loading on page load
  useEffect(() => {
    setIsFound(null);
    setPosts([]);
    setIsMore(false);
    const params = { type: searchFilter.type };
    switch (searchFilter.searchBy) {
      case SearchBy.name:
        setTags([]);
        if (searchFilter.searchValue) params.name = searchFilter.searchValue;
        break;
      case SearchBy.topic:
        setSearchFilter((state) => ({ ...state, searchValue: '' }));
        if (tags.length > 0) params.topic = tags;
        break;
      default:
        break;
    }
    getPostsRequest(params).then((data) => {
      const error_code = data.detail;
      if (error_code !== undefined) {
        if (error_code === 12) logOutRequest();
      } else {
        setIsFound(data.posts.length > 0);
        setPosts(data.posts);
        setTotal(data.total);
        if (data.posts.length !== data.total) setIsMore(true);
        setSearchFilter((state) => ({ ...state, page: state.page + 1 }));
      }
    });
    // eslint-disable-next-line
  }, [searchParams]);

  return (
    <div className='container'>
      <div className='row'>
        <h2 className='col-12 text-center mb-5 mt-lg-5'>Search</h2>
      </div>
      <div className='col-12'>
        <ControlPanel
          searchFilter={searchFilter}
          setSearchFilter={setSearchFilter}
        />
      </div>
      <div className={!tags.length ? 'mb-4' : 'mb-1'}>
        {searchFilter.searchBy === SearchBy.topic ? (
          <TagSection
            inputId='tags'
            chosenTags={tags}
            setChosenTags={setTags}
            searchMode={true}
            onSearch={handlePosts}
          />
        ) : (
          <SearchLine
            searchFilter={searchFilter}
            setSearchFilter={setSearchFilter}
            onSearch={handlePosts}
          />
        )}
      </div>
      {!posts.length && isFound === null ? (
        <PreloaderSearch />
      ) : isFound ? (
        <SearchList posts={posts} total={total} />
      ) : (
        <div className='mt-3' style={{ fontSize: '1.2rem' }}>
          Nothing found...
        </div>
      )}
      {isMore ? (
        isLoading ? (
          <PreloaderNextPage />
        ) : (
          <div className='d-flex justify-content-center'>
            <button
              type='button'
              className='btn btn-primary mb-5'
              onClick={loadNextPage}
            >
              Show more
            </button>
          </div>
        )
      ) : (
        <div className='mb-5'></div>
      )}
    </div>
  );
}
