using Genie, Genie.Router, Genie.Renderer.Html, Genie.Requests, Genie.Sessions, Random, SHA

upload_dir = "uploads"

Genie.secret_token!(sha256(randstring(256)) |> bytes2hex)
Sessions.init()

route("/") do
  sess = Sessions.session(params())
  files = Sessions.get(sess, :uploaded_files, [])
  [
    h1("Genie Filehost"),
    form(action="/upload", method="POST", enctype="multipart/form-data", () -> [
      input(type="file", name="file"),
      br(),
      input(type="submit", value="Upload")
    ]),
    Html.div([
      span("Uploaded Files:"),
      ul(map(files) do s
        li([a(s, href=s), br()])
      end)
    ])
  ] |> html
end

route("/upload", method = POST) do
  if infilespayload(:file)
    f = filespayload(:file)
    p = joinpath(upload_dir, f.name)
    if isfile(p)
      "File already exists"
    else
      write(p, f.data)
      sess = Sessions.session(params())
      files = Sessions.get(sess, :uploaded_files, [])
      push!(files, p)
      Sessions.set!(sess, :uploaded_files, files)
      redirect(p)
    end
  else
    "No file uploaded"
  end
end

route("/uploads/:file") do
  p = joinpath(upload_dir, payload(:file))
  if isfile(p)
    read(p, String)
  else
    "Not Found"
  end
end

Genie.config.server_host = "0.0.0.0"
up(8888, async=false)
