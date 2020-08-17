Bitbucket API (Asyncio)
=======================

Python Bindings for the Bitbucket API with Asyncio

The current API support coverage is very low (alpha stage).

Most calls to Bitbucket API require API credentials. You can configure them in your Bitbucket account (Personal settings / App passwords).

Installation
------------

This package is available for Python 3.6+.

.. code:: bash

    pip3 install --user .

Usage
-----

This library is based on asyncio so await/async constraints applied. To make code examples more readeable, we will omit some codes that are relevant to asyncio itself to execute a coroutine.

Initialize bitbucket API lib
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import asyncio
    from aiobitbuket.bitbucket import Bitbucket

    async def main():
        bitbucket = Bitbucket()
        bitbucket.open_basic_session(
            os.environ["BA_USER"],
            os.environ["BA_PWD"]
        )
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

Get caller permission on a specific repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    p = await bitbucket.user.permissions.repositories.get_by_full_name("croixbleue/bitbucket-management")
    print(
        "I can{} write to {} {}.".format(
            "" if p.has_write() else "'t",
            p.repository.name,
            ":)" if p.has_write() else ":("
        )
    )

Get caller permissions on all repositories not public
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    async for permission in bitbucket.user.permissions.repositories.get():
        print("{} : {}".format(
            permission.repository.name,
            permission.permission
        ))

Get repository definition from Bitbucket
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    repo = bitbucket.repositories.repo_slug("croixbleue", "b2b")
    await repo.get()
    print(repo)

Create a repository
^^^^^^^^^^^^^^^^^^^

.. code:: python

    repo = bitbucket.repositories.repo_slug("croixbleue", "aiobitbucket-wip")
    repo.project.key = "POC"
    await repo.create()

Delete the repository
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    await repo.delete()

Get All Deploy Keys
^^^^^^^^^^^^^^^^^^^

.. code:: python

    async for k in repo.deploy_keys().get():
        print(k)

Add a deploy key
^^^^^^^^^^^^^^^^

.. code:: python

    from aiobitbuket.typing.repositories import deploykey

    k : deploykey.DeployKey = repo.deploy_keys().new()
    k.key = "ssh-rsa ..."
    k.label = "test"
    await k.create()
    
    print(k.id)

Delete a specific deploy key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    await repo.deploy_keys().by_key_id(5431025).delete()

Get Pipelines configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    repo_pipelines_config = repo.pipelines_config()
    await repo_pipelines_config.get()
    print(repo_pipelines_config)

Toggle pipelines configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    repo_pipelines_config.enabled = not repo_pipelines_config.enabled
    await repo_pipelines_config.update()

Get all branch restrictions for a repository   
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    b = repo.branch_restrictions()
    async for br in b.get():
        print(br)
    
Get a branch restriction for a repository with a known id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    br = repo.branch_restrictions().by_id(10091408)
    await br.get()
    print(br)

Create a branch restriction for a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from aiobitbuket.typing.repositories import branch_restrictions

    br : branch_restrictions.BranchRestriction = repo.branch_restrictions().new()
    br.kind = branch_restrictions.Kind.RESTRICT_MERGES
    br.branch_match_kind =  branch_restrictions.BranchMatchKind.GLOB
    br.pattern = "prod"
    await br.create()

Delete a branch restriction for a repository with a known id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    br = repo.branch_restrictions().by_id(10091408)
    await br.delete()

Get all group privileges for a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Legacy 1.0 API (Not yet available on 2.0)

.. code:: python

    gp = await repo.group_privileges().get()
    print(gp)

Add group privilege for a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Legacy 1.0 API (Not yet available on 2.0)

.. code:: python

    from aiobitbuket.typing.legacy import group_privileges

    await repo.group_privileges().add("dba", group_privileges.Privilege.READ)

Delete a group privilege for a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Legacy 1.0 API (Not yet available on 2.0)

.. code:: python

    await repo.group_privileges().delete("dba")

Get all branches for a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    async for branch in repo.refs().branches.get():
        print(branch)

Get the content of a file for a commit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    # branch is an object provided by repo.refs().branches.get()
    content = await repo.src().download(branch.target.hash, "version.txt")

Create or update a pure text file (new commit)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    await repo.src().upload_pure_text(
        "/path/to/file.txt",
        "new file content\n",
        "commit message",
        "User <user@domain.tld>",
        "branch"
    )

Get all pipelines build for a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    async for pipeline in repo.pipelines().get(filter='sort=-created_on'):
        print(pipeline)
    
    # Get all successful pipelines for master branch
    async for pipeline in repo.pipelines().get(filter='sort=-created_on'):
        if pipeline.target.ref_name == "master" and \
            pipeline.state.result.name == "SUCCESSFUL":
            print(pipeline)

Error Types
-----------

About NetworkGeneric
^^^^^^^^^^^^^^^^^^^^

All Network* Exception class inherit from NetworkGeneric and are defined in errors.py file.

.. code:: python
    
    try:
        ...
    except NetworkGeneric as e:
        status, details = e.getNetworkResponse()

- 'status'
    HTTP return code (4xx or 5xx for an error, 2xx otherwise)
- 'details'
    Response payload

Exceptions
^^^^^^^^^^

- NetworkBadRequest
    Something was wrong with the client request
- NetworkUnauthorized
    Authentication is required
- NetworkForbidden
    Access to the specified resource is not permitted
- NetworkNotFound
    The requested resource does not exist
- NetworkServerErrors
    Something unexpected went wrong
- SessionAlreadyExist
    One session already exists. (Only one session should be set per bitbucket instance)
- ApiUnsupported
    Api does not support a specific network request (see api.py / ApiLeaf)
