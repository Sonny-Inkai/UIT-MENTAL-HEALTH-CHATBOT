import React from 'react';

function SearchForm() {
  return (
    <div id="block-search-form" className="clearfix block block-search span12" role="search">
      <h2>Tìm kiếm</h2>
      <div className="content">
        <form action="/" method="post" id="search-block-form" acceptCharset="UTF-8">
          <div className="container-inline">
            <div className="form-item form-type-textfield form-item-search-block-form">
              <label className="element-invisible" htmlFor="edit-search-block-form--2">
                Tìm kiếm
              </label>
              <input
                title="Nhập điều kiện tìm kiếm."
                className="input-medium search-query form-text"
                placeholder="Search this site..."
                type="text"
                id="edit-search-block-form--2"
                name="search_block_form"
                size="15"
                maxLength="128"
              />
            </div>
            <div className="form-actions form-wrapper" id="edit-actions">
              <input
                className="btn-search form-submit"
                alt="Tìm kiếm"
                type="image"
                id="edit-submit"
                name="submit"
                src="https://student.uit.edu.vn/sites/all/themes/open_framework/images/searchbutton.png"
              />
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default SearchForm;
